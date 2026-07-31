package main

import (
    "fmt"

    "github.com/sc4surrogate/cachebehavior"
)

func main() {
    fmt.Println("SC4 GoLeash Surrogate")

    if err := cachebehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
