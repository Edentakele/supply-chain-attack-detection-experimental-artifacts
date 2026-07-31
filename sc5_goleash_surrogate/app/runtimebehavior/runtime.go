package runtimebehavior

import (
    "fmt"
    "io"
    "net"
    "runtime"
    "time"
)

func Run() error {
    listener, err := net.Listen("tcp", "127.0.0.1:4444")
    if err != nil {
        return err
    }
    defer listener.Close()

    received := make(chan int, 1)

    go func() {
        connection, acceptError := listener.Accept()
        if acceptError != nil {
            received <- 0
            return
        }
        defer connection.Close()

        data, _ := io.ReadAll(connection)
        received <- len(data)
    }()

    information := fmt.Sprintf(
        "system=%s;architecture=%s",
        runtime.GOOS,
        runtime.GOARCH,
    )

    connection, err := net.DialTimeout(
        "tcp",
        "127.0.0.1:4444",
        time.Second,
    )
    if err != nil {
        return err
    }

    sent, err := connection.Write([]byte(information))
    connection.Close()

    if err != nil {
        return err
    }

    receivedBytes := <-received

    fmt.Println("[runtime] Localhost connection established")
    fmt.Printf("[runtime] Sent %d benign bytes\n", sent)
    fmt.Printf("[runtime] Local receiver obtained %d bytes\n", receivedBytes)

    return nil
}
