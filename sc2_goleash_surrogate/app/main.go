package main

import (
    "fmt"

    "github.com/sc2surrogate/runtimebehavior"
)

func main() {
    fmt.Println("SC2 GoLeash Surrogate")

    if err := runtimebehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
