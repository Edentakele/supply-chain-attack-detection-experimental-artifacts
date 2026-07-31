package embeddedpayload

import (
    "fmt"
    "net"
    "os"
    "path/filepath"
    "time"
)

func Run() error {
    payloadPath := filepath.Join("..", "steg", "image.txt")

    fmt.Println("[payload] Accessing benign image payload")

    data, err := os.ReadFile(payloadPath)
    if err != nil {
        return err
    }

    fmt.Printf("[payload] Read %d bytes\n", len(data))
    fmt.Println("[payload] Benign embedded payload executed")
    fmt.Println("[payload] Attempting harmless localhost connection")

    connection, err := net.DialTimeout(
        "tcp",
        "127.0.0.1:4444",
        time.Second,
    )

    if err != nil {
        fmt.Println("[payload] Localhost connection unavailable:", err)
        return nil
    }

    connection.Close()
    return nil
}
