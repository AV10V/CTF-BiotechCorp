# CTF · BiotechCorp

Interactive walkthrough of a three-host Active Directory lab — from a single handed-over
account (`e.ross`) to Domain Admin.

**Live page:** <https://av10v.github.io/CTF-BiotechCorp/>

## The path

```
attacker@AV10V-mac  →  Kali VM  →  OpenVPN  →  DB26 192.168.197.180
                                                      ↓ chisel SOCKS5
                                              DC20 172.16.197.200
                                                      ↓ WinRM
                                             MGMT22 172.16.197.202
```

## How each box fell

| Host | Access | What gave it up |
|---|---|---|
| **DB26** `192.168.197.180` | `e.ross` over MSSQL Windows auth, then `xp_cmdshell` | Devs-share keytab (RC4 for `z.patterson`), DSC MOF with a cleartext service password |
| **DC20** `172.16.197.200` | gMSA AES256 → WinRM → two ACL hops → ADCS ESC3 | Enrollment-agent template enrollable by one Certificate Manager → on-behalf-of `a.r.andrews` → Domain Admin |
| **MGMT22** `172.16.197.202` | `svc-mgmt` (Remote Management Users) | Flag read with the Domain Admin ticket |

Flags: `DB26` was collected straight from `xp_cmdshell` (first objective); `DC20` and `MGMT22`
after Domain Admin.

## Page contents

- **Topology** — clickable boxes from the Mac through the pivot to each target
- **Step-by-step** — ten steps, arrow-key navigable, with the real commands and copy buttons
- **Loot** — click-to-reveal credential table and all three flags

Single self-contained `index.html` — no external JS, CSS or fonts.

## Note on secrets

Credentials, hashes and flags belong to one completed lab instance. The range is intentionally
vulnerable; rotate everything if you reuse it.
