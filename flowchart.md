%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e1f5fe', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
graph TD
    %% --- Data Sources (Inputs) ---
    subgraph Inside_Package [Internal Sensors (IoT)]
        T_int[DHT22: Internal Temp Sensor]
        Load_Cell[Load Cell: PCM Mass Sensor]
    end

    subgraph External_Sources [External APIs & Sensors]
        GPS[GPS Module: Location Data]
        T_amb[External Temp Sensor]
    end

    subgraph Cloud_API [Cloud Data Services]
        Traffic_API(Google Maps API: Traffic Speed)
        Weather_API(OpenWeather API: Forecast)
    end

    %% --- Data Processing Network ---
    MCU[MCU: ESP32 / Micro-controller]
    MQTT[MQTT Protocol: Data Transmission]
    
    subgraph AI_Core [AI Predictive Engine (Edge/Cloud)]
        LSTM[LSTM Model: Thermal Decay Prediction]
        Data_Fusion[Data Fusion: Sensor Correlation]
    end

    %% --- Decision & Output ---
    RBA_Calc[RBA Calculation: Remaining Bio-Autonomy]
    HMI[HMI: Touchscreen Display]
    Alert[Alert System: Critical Warning]

    %% --- Flow Connections ---
    Inside_Package --> MCU
    External_Sources --> MCU
    Cloud_API -.->|WiFi/4G| MQTT
    MCU -->|Publish| MQTT
    MQTT -->|Subscribe| AI_Core
    
    Data_Fusion --> LSTM
    AI_Core --> RBA_Calc
    RBA_Calc -->|Result| MQTT
    MQTT -->|Display Data| MCU
    MCU --> HMI
    RBA_Calc -->|Threshold Trigger| Alert

    %% --- Styling ---
    classDef source fill:#bbdefb,stroke:#1565c0,stroke-width:2px;
    classDef proc fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef ai fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px,stroke-dasharray: 5 5;
    classDef out fill:#ffccbc,stroke:#e64a19,stroke-width:2px;

    class T_int,Load_Cell,GPS,T_amb,Traffic_API,Weather_API source;
    class MCU,MQTT,Data_Fusion,RBA_Calc proc;
    class LSTM,AI_Core ai;
    class HMI,Alert out;%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e1f5fe', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
graph TD
    %% --- Data Sources (Inputs) ---
    subgraph Inside_Package [Internal Sensors (IoT)]
        T_int[DHT22: Internal Temp Sensor]
        Load_Cell[Load Cell: PCM Mass Sensor]
    end

    subgraph External_Sources [External APIs & Sensors]
        GPS[GPS Module: Location Data]
        T_amb[External Temp Sensor]
    end

    subgraph Cloud_API [Cloud Data Services]
        Traffic_API(Google Maps API: Traffic Speed)
        Weather_API(OpenWeather API: Forecast)
    end

    %% --- Data Processing Network ---
    MCU[MCU: ESP32 / Micro-controller]
    MQTT[MQTT Protocol: Data Transmission]
    
    subgraph AI_Core [AI Predictive Engine (Edge/Cloud)]
        LSTM[LSTM Model: Thermal Decay Prediction]
        Data_Fusion[Data Fusion: Sensor Correlation]
    end

    %% --- Decision & Output ---
    RBA_Calc[RBA Calculation: Remaining Bio-Autonomy]
    HMI[HMI: Touchscreen Display]
    Alert[Alert System: Critical Warning]

    %% --- Flow Connections ---
    Inside_Package --> MCU
    External_Sources --> MCU
    Cloud_API -.->|WiFi/4G| MQTT
    MCU -->|Publish| MQTT
    MQTT -->|Subscribe| AI_Core
    
    Data_Fusion --> LSTM
    AI_Core --> RBA_Calc
    RBA_Calc -->|Result| MQTT
    MQTT -->|Display Data| MCU
    MCU --> HMI
    RBA_Calc -->|Threshold Trigger| Alert

    %% --- Styling ---
    classDef source fill:#bbdefb,stroke:#1565c0,stroke-width:2px;
    classDef proc fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef ai fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px,stroke-dasharray: 5 5;
    classDef out fill:#ffccbc,stroke:#e64a19,stroke-width:2px;

    class T_int,Load_Cell,GPS,T_amb,Traffic_API,Weather_API source;
    class MCU,MQTT,Data_Fusion,RBA_Calc proc;
    class LSTM,AI_Core ai;
    class HMI,Alert out;