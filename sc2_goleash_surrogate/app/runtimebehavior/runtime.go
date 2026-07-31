package runtimebehavior

import (
    "fmt"
    "net"
    "time"
)

func Run() error {
    fmt.Println("[runtime] Installed payload executing")
    fmt.Println("[runtime] Attempting harmless localhost connection")

    connection, err := net.DialTimeout(
        "tcp",
        "127.0.0.1:4444",
        time.Second,
    )

    if err != nil {
        fmt.Println("[runtime] Localhost connection unavailable:", err)
        return nil
    }

    connection.Close()
    return nil
}
