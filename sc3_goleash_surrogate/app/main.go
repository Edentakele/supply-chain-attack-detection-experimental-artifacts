package main

import (
    "fmt"

    "github.com/sc3surrogate/runtimebehavior"
)

func main() {
    fmt.Println("SC3 GoLeash Surrogate")

    if err := runtimebehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
