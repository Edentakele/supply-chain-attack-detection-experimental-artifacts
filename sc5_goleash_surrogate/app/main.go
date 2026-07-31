package main

import (
    "fmt"

    "github.com/sc5surrogate/runtimebehavior"
)

func main() {
    fmt.Println("SC5 GoLeash Surrogate")

    if err := runtimebehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
