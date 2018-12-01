import fileinput

print(sum(int(term) for term in fileinput.input()))
