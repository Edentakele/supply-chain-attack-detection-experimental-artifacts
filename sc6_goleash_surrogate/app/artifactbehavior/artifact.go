package artifactbehavior

import (
    "archive/zip"
    "fmt"
    "os"
    "path/filepath"
)

func Run() error {
    outputDirectory := filepath.Join("..", "artifact")

    if err := os.MkdirAll(outputDirectory, 0755); err != nil {
        return err
    }

    outputPath := filepath.Join(
        outputDirectory,
        "build_artifact.zip",
    )

    outputFile, err := os.Create(outputPath)
    if err != nil {
        return err
    }

    archiveWriter := zip.NewWriter(outputFile)

    entry, err := archiveWriter.Create("build_config.py")
    if err != nil {
        outputFile.Close()
        return err
    }

    if _, err := entry.Write(
        []byte("BUILD_MODE = \"instrumented\"\n"),
    ); err != nil {
        outputFile.Close()
        return err
    }

    if err := archiveWriter.Close(); err != nil {
        outputFile.Close()
        return err
    }

    if err := outputFile.Close(); err != nil {
        return err
    }

    fmt.Println("[runtime] Build artifact package created")
    return nil
}
