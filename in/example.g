K := SymmetricGroup(5);
# Comments are rendered.
# Output is not rendered if the input ends on `;;`.
H := SymmetricGroup(8);;
G := WreathProduct(K, H);
# Long output is rendered with automatic linebreaks
# as produced by a normal GAP session with linelength `80`.
g := PseudoRandom(G);
# Linebreaks in the input file are respected.
A := DirectProduct([
    SymmetricGroup(7),
    SymmetricGroup(4),
    AlternatingGroup(6),
]);
# Empty lines are rendered as well.

# Like the empty line above this comment.
B := "This is a long line which has to be split manually in order to prevent overfloats!";;
# It is advised to only use at most 80 characters per line.
# You can also read files from within a session
Read("lib/dependency.g");;
foo(3);