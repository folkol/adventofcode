fish = [int(s) for s in input().split(',')]

N = 256
dp = [[0, 0] for _ in range(N + 10)]  # state: [fish, fishlings] * days
dp[0][0] = len(fish)
for n in fish:
    for m in range(n + 1, N + 1, 7):
        dp[m][1] += 1

for n in range(1, N + 1 + 9):
    dp[n][0] = dp[n - 1][0] + dp[n][1]
    for m in range(n + 9, N + 1, 7):
        dp[m][1] += dp[n][1]

print(dp[N][0])
