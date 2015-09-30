#!yaml|gpg

environment: production

domain: tracpro.io

repo:
  url: git@github.com:rapidpro/tracpro.git
  branch: master

# Additional public environment variables to set for the project
env:
  CSRF_COOKIE_DOMAIN: ".tracpro.io"
  HOSTNAME: "tracpro.io"
  SESSION_COOKIE_DOMAIN: ".tracpro.io"
  SITE_HOST_PATTERN: "https://%s.tracpro.io"

# Private environment variables.
# Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAzBv9PsbguWNAQf+O2oj9juZbpRcbCBMD8wfvjWBi3GZCVd1pfYPmQdktCU1
    ih77O7MPn3DDQVcfZ1lYr9pETf2mprMdk0ytUzLsBjzGrA2mmvPJRQZZNJQqqiDP
    xjIk8/NwSHD5I4u25K3wK0DCnUWb6xGLAObSoengXctWDLaxnrt3HVLSw0yXXCqk
    dBva4rdAqxwS0p5zoqRlatqdmieg3zPorW+dPVNKk+mL0MvS0OQznoktPwThshfV
    Z7dc7g0FW9UAKliZxodnvtG+B2F1Rpz+aNOSqjdu42Eh+UlFvOS9BUTrRdaUUq+h
    UhqGhnZOfHFGPOvafFKraKsunxprR4ihJKfnDtf78NJJAZuU1rHGC1WaLhs2ZEUN
    RsIxXoDHskhxvkV0nxrsIfgCzK3U6DmTyy9yexvSRdDQGP1BmSgwnikp8QYzDtmF
    KD7j8YpCnxRrvg==
    =S7Lq
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAzBv9PsbguWNAQf/ROPyLLBgdMx6j63RBdYGCLeARJJqF3wm9NgnQeGHez4w
    Rfh9BR8yZABv4djqI9FMVJlkW7O4LvG2dIjfTVXtJmEGpnMg1sooB8jHJ/J8El2O
    4uj+ZmQ4LNYUW5UZHFGHPnzZTi8rrmRSgCxQBO2ZLFLC8MlWxyqXivM9gbLI+hPr
    gf/1JJvqCHdAcCw/ey40rq7dFk5Mj5mcp+K8jYw0u+Hocw/C/C38PkSET6e6hieV
    W/w+gzXZI0Foc8IE5NweiUql/f2wkthfO8M6mAi8Z6GI/lYXLeROBzxnIvz2LY5g
    FjEj1uTZi4mUFnKU2uc4wewxkzqBeQRdobp1YHb4JdJ7AYBuz7GEZaKstH2aljSC
    yCel3fy7PJO8xbsht4S/Hp/JoMPL6MApzq8DtSRoPPtCSKFEroDq1QDW1SEQYgUh
    X65z45cw9yreT+y+dAOei6WIAN6HkkliiMxIrHSOCphpghAArOs6LIWxdkdm1wat
    qsSRCTgqWcOq1DM4
    =JNt9
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAzBv9PsbguWNAQf/brJN90xKdHjTOG8X8t00ex7oOGa9H62JotBKTcyKz3Dq
    Zfp4MkCy6MrbKHVV6nzv9PfX/miydtMLdnJzKqj4K9LRB+ndXDsb3aEfxJY0Qtop
    GiRfY2YuJOw2bP5QtPfMtMTWRWllnwT15SZflRXo8UyAFjO9CyZ0vfoMkkNznbsv
    a+D3TINSbiJU3nYyLwennRA3aRsrRbfk3lSaNSu5PtEPERddciAPcF2G0XKxZfhA
    x/rMWIkD4da4s+WyIGSdI5qpyEgsq1bC+t6Mn0rmC500kHSysh6sccM/rG0CIMBS
    tIrKxV5hZ/St5AMiDLdmEYnoe1HWOOzKopcOnJ4SAtJJAS23bczKIhxJ2OvRe24t
    EWt+Co93S5n3cqa42VIpqhyPOgqN0FZdmtny9B669waxFUN7WmJGbvJ5P3nJGTOs
    9gxxa8RS+DJ9dw==
    =AH05
    -----END PGP MESSAGE-----

# Private deploy key. Must be GPG encrypted.
github_deploy_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =aQpO
  -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
# {% if 'balancer' in grains['roles'] %}
ssl_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =+SBO
  -----END PGP MESSAGE-----

ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =wv22
  -----END PGP MESSAGE-----
# {% endif %}
