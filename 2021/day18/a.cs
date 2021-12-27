using System;
using System.Text.RegularExpressions;

namespace AoC
{
    interface Node
    {
        static (Node, int) Parse(string line, int pos = 0)
        {
            if (line[pos] == '[')
            {
                Node left, right;
                (left, pos) = Parse(line, pos + 1);
                (right, pos) = Parse(line, pos + 1);
                return (new Pair(left, right), pos + 1);
            }
            else
            {
                var n = line.Substring(pos);
                var match = Regex.Match(n, @"^(\d+)");
                if (!match.Success)
                {
                    throw new Exception($"Expected number, found: '{n}'.");
                }
                var group = match.Groups[0];
                return (new Number(Int32.Parse(group.Value)), pos + group.Length);
            }
        }

        static Node Add(Node a, Node b)
        {
            var result = new Pair(a, b);
            result.Reduce();
            return result;
        }

        int Magnitude();
    }
    internal class Pair : Node
    {
        internal Node left { set; get; }
        internal Node right { set; get; }

        internal Pair(Node left, Node right)
        {
            this.left = left;
            this.right = right;
        }

        int Node.Magnitude()
        {
            return 3 * left.Magnitude() + 2 * right.Magnitude();
        }

        internal void Reduce()
        {
            (bool, Number, int) Explode(Node tree, bool did_explode = false, Number left_number = null, int right_carry = 0, int nesting = 0)
            {
                if (nesting == 4 && !did_explode && tree is Pair)
                {
                    var pair = tree as Pair;
                    if (left_number != null && pair.left is Number)
                    {
                        var pair_left = pair.left as Number;
                        left_number.value += pair_left.value;
                    }
                    var pair_right = pair.right as Number;
                    return (true, left_number, pair_right.value);
                }
                if (tree is Pair)
                {
                    var pair = tree as Pair;
                    var (left, right) = (pair.left, pair.right);
                    var was_exploded = did_explode;
                    (did_explode, left_number, right_carry) = Explode(left, did_explode, left_number, right_carry, nesting + 1);
                    if (nesting == 3 && !was_exploded && did_explode)
                    {
                        pair.left = new Number(0);
                        did_explode = true;
                    }
                    was_exploded = did_explode;
                    (did_explode, left_number, right_carry) = Explode(right, did_explode, left_number, right_carry, nesting + 1);
                    if (nesting == 3 && !was_exploded && did_explode)
                    {
                        pair.right = new Number(0);
                        did_explode = true;
                    }
                }
                else
                {
                    var number = tree as Number;
                    if (right_carry > 0)
                    {
                        number.value += right_carry;
                        right_carry = 0;
                    }
                    left_number = number;
                }
                return (did_explode, left_number, right_carry);

            }

            bool Split(Node node)
            {
                if (node is Pair)
                {
                    var pair = node as Pair;
                    var (left, right) = (pair.left, pair.right);
                    if (left is Number)
                    {
                        var leftNumber = left as Number;
                        if (leftNumber.value > 9)
                        {
                            pair.left = new Pair(new Number(leftNumber.value / 2), new Number((leftNumber.value + 1) / 2));
                            return true;
                        }
                    }
                    var did_split = Split(left);
                    if (did_split)
                    {
                        return true;
                    }
                    if (right is Number)
                    {
                        var rightNumber = right as Number;
                        if (rightNumber.value > 9)
                        {
                            pair.right = new Pair(new Number(rightNumber.value / 2), new Number((rightNumber.value + 1) / 2));
                            return true;
                        }
                    }
                    return Split(right);
                }
                return false;
            }

            while (true)
            {
                var (did_explode, _, _) = Explode(this);
                if (did_explode)
                {
                    continue;
                }
                if (Split(this))
                {
                    continue;
                }
                break;
            }
        }

        public override string ToString()
        {
            return $"[{left}, {right}]";
        }
    }

    class Number : Node
    {
        internal int value { set; get; }

        internal Number(int value)
        {
            this.value = value;
        }

        int Node.Magnitude()
        {
            return value;
        }

        public override string ToString()
        {
            return value.ToString();
        }
    }

    class Day18
    {
        static void Main(string[] args)
        {
            Node result = null;
            foreach (string line in System.IO.File.ReadLines(@"input.dat"))
            {
                var (node, _) = Node.Parse(line);
                if (result == null)
                {
                    result = node;
                }
                else
                {
                    result = Node.Add(result, node);
                }
            }

            Console.WriteLine(result.Magnitude());
            Console.Out.Flush();
        }
    }
}