package main

import (
    "fmt"

    "github.com/sc6surrogate/artifactbehavior"
)

func main() {
    fmt.Println("SC6 GoLeash Surrogate")

    if err := artifactbehavior.Run(); err != nil {
        fmt.Println("[runtime] Error:", err)
    }
}
