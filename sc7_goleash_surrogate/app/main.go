package main

import (
    "fmt"

    "github.com/sc7surrogate/runtimebehavior"
)

func main() {
    fmt.Println("SC7 GoLeash Surrogate")

    if err := runtimebehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
