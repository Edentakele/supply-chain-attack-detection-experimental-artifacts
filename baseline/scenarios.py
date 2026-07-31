SCENARIOS = {
    "SC1": {
        "ground_truth": [
            "install",
            "payload_access",
            "payload_execution",
            "outbound_connection",
        ],
        "directories": [
            "../sc1_foreman_surrogate",
            "../sc1_goleash_surrogate",
        ],
        "rules": {
            "payload_execution.marker": "payload_execution",
        },
    },
    "SC2": {
        "ground_truth": [
            "install",
            "persistence_setup",
            "file_replacement",
            "payload_installation",
            "runtime_execution",
            "outbound_connection",
        ],
        "directories": [
            "../sc2_foreman_surrogate",
            "../sc2_goleash_surrogate",
        ],
        "rules": {
            "sc2_autostart.conf": "persistence_setup",
            "installed_payload.txt": "payload_installation",
        },
    },
    "SC3": {
        "ground_truth": [
            "install",
            "file_collection",
            "archive_creation",
            "outbound_connection",
            "exfiltration",
        ],
        "directories": [
            "../sc3_foreman_surrogate",
            "../sc3_goleash_surrogate",
        ],
        "rules": {
            "archive.zip": "archive_creation",
        },
    },
    "SC4": {
        "ground_truth": [
            "install",
            "download",
            "outbound_connection",
            "exfiltration",
        ],
        "directories": [
            "../sc4_foreman_surrogate",
            "../sc4_goleash_surrogate",
        ],
        "rules": {
            "payload.js": "download",
        },
    },
    "SC5": {
        "ground_truth": [
            "install",
            "download",
            "outbound_connection",
            "exfiltration",
        ],
        "directories": [
            "../sc5_foreman_surrogate",
            "../sc5_goleash_surrogate",
        ],
        "rules": {
            "payload.bin": "download",
        },
    },
    "SC6": {
        "ground_truth": [
            "credential_exposure",
            "build_modification",
            "artifact_packaging",
            "publishing",
        ],
        "directories": [
            "../sc6_foreman_surrogate",
            "../sc6_goleash_surrogate",
        ],
        "rules": {
            "build_artifact.zip": "artifact_packaging",
        },
    },
    "SC7": {
        "ground_truth": [
            "download",
            "outbound_connection",
            "exfiltration",
        ],
        "directories": [
            "../sc7_foreman_surrogate",
            "../sc7_goleash_surrogate",
        ],
        "rules": {
            "model_payload.bin": "download",
        },
    },
}
