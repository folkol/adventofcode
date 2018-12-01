import fileinput

frequency_deltas = (int(term) for term in fileinput.input())
print(sum(frequency_deltas))
