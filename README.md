# lab6-portscanner

Laboratorijska vježba 6 — Skener portova

Jednostavan TCP port skener napisan u Pythonu koristeći isključivo ugrađeni `socket` modul. Podržava skeniranje jednog porta, raspona portova i više hostova istovremeno. Koristi višenitno izvođenje za brže skeniranje.

## Datoteke

- `port_scanner.py` — glavni skript

## Kako pokrenuti

### Zadatak 1 — jedan port

```bash
python3 port_scanner.py --hosts 127.0.0.1 --port 2222
python3 port_scanner.py --hosts scanme.nmap.org --port 80
python3 port_scanner.py --hosts portquiz.net --port 443
```

### Zadatak 2 — raspon portova

```bash
python3 port_scanner.py --hosts 127.0.0.1 --range 20 1024
python3 port_scanner.py --hosts scanme.nmap.org --range 20 1024
```

### Zadatak 3 — više hostova

```bash
python3 port_scanner.py --hosts 127.0.0.1,scanme.nmap.org --range 20 1024
```

## Opcije

| Opcija | Kratka | Opis | Zadano |
|--------|--------|------|--------|
| `--hosts` | `-H` | Comma-odvojena lista hostova | obavezno |
| `--port` | `-p` | Jedan port (1–65535) | — |
| `--range START END` | — | Raspon portova (inclusive) | — |
| `--timeout` | `-t` | Timeout po portu u sekundama | `0.5` |
| `--workers` | `-w` | Broj paralelnih niti | `100` |

## Primjeri izlaza

### Jedan port — otvoren

```
$ python3 port_scanner.py --hosts 127.0.0.1 --port 2222
Scanning 127.0.0.1 (127.0.0.1) ports 2222-2222
Open ports on 127.0.0.1:
 - 2222 (EtherNetIP-1)
```

### Jedan port — zatvoren

```
$ python3 port_scanner.py --hosts 127.0.0.1 --port 9999
Scanning 127.0.0.1 (127.0.0.1) ports 9999-9999
No open TCP ports found on 127.0.0.1 in the scanned range.
```

### Raspon portova na scanme.nmap.org

```
$ python3 port_scanner.py --hosts scanme.nmap.org --range 20 1024
Scanning scanme.nmap.org (45.33.32.156) ports 20-1024
Open ports on scanme.nmap.org:
 - 22 (ssh)
 - 80 (http)
```

### Više hostova

```
$ python3 port_scanner.py --hosts 127.0.0.1,scanme.nmap.org --range 20 1024
Scanning 127.0.0.1 (127.0.0.1) ports 20-1024
No open TCP ports found on 127.0.0.1 in the scanned range.

Scanning scanme.nmap.org (45.33.32.156) ports 20-1024
Open ports on scanme.nmap.org:
 - 22 (ssh)
 - 80 (http)
```

## Testirani portovi

| Host | Port | Status | Servis |
|------|------|--------|--------|
| `127.0.0.1` | 2222 | otvoren | SSH |
| `scanme.nmap.org` | 22 | otvoren | SSH |
| `scanme.nmap.org` | 80 | otvoren | HTTP |
| `portquiz.net` | 80 | otvoren | HTTP |
| `portquiz.net` | 443 | otvoren | HTTPS |
| `portquiz.net` | 8080 | otvoren | http-alt |

> Testni hostovi `scanme.nmap.org` i `portquiz.net` su javni serveri predviđeni za ovakve testove. 