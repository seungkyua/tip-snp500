# crontab 등록

- 유저 계정: `ask`
- python 스크립트 위치: `/home/ask/works/tip-snp500/main.py`

```
sudo crontab -e

* * * * * su - ask -c "/usr/bin/python3 /home/ask/works/tip-snp500/main.py"
```