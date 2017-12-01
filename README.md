# Hackish solutions to adventofcode.com 2017

## Day 1

```
$ jot -n -s '' -r 100000000 0 9 > captcha
$ time python3 a1.py <captcha
$
$ cc -Ofast captcha.c -o captcharoo
$ time ./captcharoo <captcha
```

