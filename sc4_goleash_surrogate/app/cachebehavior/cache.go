package cachebehavior

import (
    "fmt"
    "os"
    "path/filepath"
    "runtime"
)

func Run() error {
    outputDirectory := filepath.Join("..", "exfil")

    if err := os.MkdirAll(outputDirectory, 0755); err != nil {
        return err
    }

    systemInfo := fmt.Sprintf(
        "system=%s\nmachine=%s\n",
        runtime.GOOS,
        runtime.GOARCH,
    )

    outputPath := filepath.Join(
        outputDirectory,
        "system_info.txt",
    )

    if err := os.WriteFile(
        outputPath,
        []byte(systemInfo),
        0644,
    ); err != nil {
        return err
    }

    fmt.Println("[runtime] Benign information written to local output")
    return nil
}
