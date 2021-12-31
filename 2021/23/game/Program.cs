using Terminal.Gui;


namespace vmproject.ui
{
    class Program
    {
        static List<string> testGame = new List<string> {
                "#############",
                "#...........#",
                "###B#C#B#D###",
                "  #A#D#C#A#  ",
                "  #########  ",
                "",
                ""};

        static List<string> realGame = new List<string> {
                "#############",
                "#...........#",
                "###C#B#A#D###",
                "  #B#C#D#A#  ",
                "  #########  ",
                "",
                ""};
        
        static List<string> realGame2 = new List<string> {
                "#############",
                "#...........#",
                "###C#B#A#D###",
                "  #D#C#B#A#  ",
                "  #D#B#A#C#  ",
                "  #B#C#D#A#  ",
                "  #########  "};

        static int energyUsed = 0;
        static bool moveMode = false;
        static bool renderRequired = false;
        static bool popRequired = false;
        static string testMode = "test";
        static Point newTo = new Point(0, 0);
        static TextView gameArea = null;
        static TextView statusArea = null;
        static readonly Dictionary<char, int> podMoveCosts = new Dictionary<char, int> {
              {'A', 1},
              {'B', 10},
              {'C', 100},
              {'D', 1000}
            };

        static Dictionary<Key, Point> arrowKeys = new Dictionary<Key, Point> {
            {Key.CursorDown, new Point(0, 1)},
            {Key.CursorLeft, new Point(-1, 0)},
            {Key.CursorRight, new Point(1, 0)},
            {Key.CursorUp, new Point(0, -1)}
        };

        static char[][] gameData = testGame.Select(l => l.ToCharArray()).ToArray();

        static Stack<Tuple<char[][], int, Point>> undoStack = new Stack<Tuple<char[][], int, Point>>();

        static void UpdateStatus()
        {
            statusArea.Text = $"Mode: {(moveMode ? "move" : "select")}\nEnergy used: {energyUsed}\nGame: {testMode}";
        }

        static void DoMove(Point from, Point to) {
            if ((Math.Abs(from.X - to.X) + Math.Abs(from.Y - to.Y)) == 1) {
                var fromChar = gameData[from.Y][from.X];
                var toChar = gameData[to.Y][to.X];
                if (podMoveCosts.Keys.Contains(fromChar) && toChar == '.') {
                    var undoGameData = gameData.Select(l => l.Select(c => c).ToArray()).ToArray();
                    undoStack.Push(Tuple.Create(undoGameData, energyUsed, new Point(from.X, from.Y)));
                    gameData[to.Y][to.X] = fromChar;
                    gameData[from.Y][from.X] = '.';
                    energyUsed += podMoveCosts[fromChar];
                    newTo = to;
                    renderRequired = true;
                }
            }
        }
        static void Main(string[] args)
        {
            Application.Init();
            var top = Application.Top;

            var win = new Window("Sort Amphipods")
            {
                X = 0,
                Y = 1,
                Width = Dim.Fill(),
                Height = Dim.Fill()
            };
            top.Add(win);

            var loadNew = (string input) => {
                if (input == "test") 
                    gameData = testGame.Select(l => l.ToCharArray()).ToArray();
                else if (input == "part 1")
                    gameData = realGame.Select(l => l.ToCharArray()).ToArray();
                else
                    gameData = realGame2.Select(l => l.ToCharArray()).ToArray();
                moveMode = false;
                renderRequired = false;
                energyUsed = 0;
                testMode = input;
                undoStack.Clear();
                gameArea.Text = String.Join("\n", gameData.Select(l => String.Join("", l)));
                UpdateStatus();
            };

            var menu = new MenuBar(new MenuBarItem[] {
                new MenuBarItem ("_File", new MenuItem [] {
                    new MenuItem ("Load test", "", () => { loadNew("test"); }),
                    new MenuItem ("Load part 1", "", () => { loadNew("part 1"); }),
                    new MenuItem ("Load part 2", "", () => { loadNew("part 2"); }),
                    new MenuItem ("Quit", "", () => { top.Running = false; })
                  
                }),
              });
            top.Add(menu);

            var statusFrame = new FrameView("Status")
            {
                AutoSize = true,
                X = gameData[0].Length + 10,
                Y = 2,
                Width = 22,
                Height = gameData.Length + 4
            };

            statusArea = new TextView(
                new Rect(1, 1, 20, gameData.Length))
            {
                ReadOnly = true
            };

            statusFrame.Add(statusArea);
            win.Add(statusFrame);

            var gameFrame = new FrameView("Game Area")
            {
                AutoSize = true,
                X = 2,
                Y = 2,
                Width = gameData[0].Length + 4,
                Height = gameData.Length + 4
            };

            gameArea = new TextView(
                new Rect(1, 1, gameData[0].Length, gameData.Length))
            {
                Text = String.Join("\n", gameData.Select(l => String.Join("", l))),
                ReadOnly = true
            };
            gameFrame.Add(gameArea);
            win.Add(gameFrame);

            Action<View.KeyEventEventArgs> KeyDownHandler = (e) =>
            {
                if (gameArea.HasFocus) {
                    var key = e.KeyEvent.Key;
                    if (arrowKeys.Keys.Contains(e.KeyEvent.Key) && moveMode) {
                        var from = gameArea.CursorPosition;
                        var to = new Point(from.X + arrowKeys[e.KeyEvent.Key].X, from.Y + arrowKeys[e.KeyEvent.Key].Y);
                        if (to.X >= 0 && to.X < gameData[0].Length && to.Y >= 0 && to.Y < gameData.Length)
                            DoMove(from, to);
                    }
                    else if (e.KeyEvent.KeyValue == (int)'m')
                    {
                        moveMode = !moveMode;
                    }
                    else if (e.KeyEvent.KeyValue == (int)'z' && undoStack.Any())
                    {
                        renderRequired = popRequired = true;
                    }
                    UpdateStatus();
                }
            };

            win.KeyDown += KeyDownHandler;
            win.KeyUp += (e) => {
                if (renderRequired) {
                    if (popRequired) {
                        (gameData, energyUsed, newTo) = undoStack.Pop();
                    }
                    gameArea.Text = String.Join("\n", gameData.Select(l => String.Join("", l)));
                    gameArea.CursorPosition = newTo;
                    UpdateStatus();
                    renderRequired = false;
                    popRequired = false;
                }
            };

            gameArea.SetFocus();
            gameArea.CursorPosition = newTo;
            UpdateStatus();
            Application.Run();
        }
    }
}