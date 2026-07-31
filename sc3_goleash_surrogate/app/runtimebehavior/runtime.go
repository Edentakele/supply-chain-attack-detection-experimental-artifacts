package runtimebehavior

import (
    "fmt"
    "net"
    "os"
    "path/filepath"
    "time"
)

func Run() error {
    source := filepath.Join("..", "data", "system_info.txt")

    data, err := os.ReadFile(source)
    if err != nil {
        return err
    }

    fmt.Printf("[runtime] Collected %d bytes from benign input file\n", len(data))
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
