#!/usr/bin/expect -f

spawn nano /etc/modules-load.d/ec_sys.conf
send "\nec_sys\n"
send "\x1B"         ;# Escape key
send "\x13"         ;# Ctrl+S
send "\x0D"         ;# Enter
send "\x18"         ;# Ctrl+X
expect {
    "Save modified buffer*" { send "Y\r" }
    eof
}
send "\x0D"         ;# Enter
send "\x1B"         ;# Escape key
expect eof