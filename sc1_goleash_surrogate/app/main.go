package main

import (
    "fmt"

    "github.com/sc1surrogate/embeddedpayload"
)

func main() {
    fmt.Println("SC1 GoLeash Surrogate - Benign Application")

    if err := embeddedpayload.Run(); err != nil {
        fmt.Println("[payload] Error:", err)
    }
}
