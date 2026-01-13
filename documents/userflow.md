```mermaid
graph TD
    %% スタイル定義
    classDef user fill:#f9f,stroke:#333,stroke-width:2px,color:black;
    classDef platform fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,color:black;
    classDef plugin fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,stroke-dasharray: 5 5,color:black;
    classDef agent fill:#ffecb3,stroke:#ffa000,stroke-width:2px,color:black;
    classDef llm fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:black;

    User((👤 You / User)):::user

    subgraph Terminal_Environment [💻 Your Terminal / Server]
        
        subgraph OpenCode_Platform [🏢 OpenCode (The Platform/OS)]
            direction TB
            desc_oc[("<b>基盤機能</b><br>・ファイル操作 (I/O)<br>・API通信管理<br>・ツール実行 (LSP/Grep)")]:::platform
            
            subgraph Oh_My_OpenCode [🚀 Oh My OpenCode (The Expert Team)]
                direction TB
                
                Sisyphus[("<b>🎩 Sisyphus (PM/Lead)</b><br>役割: タスク管理・実装<br>Brain: <b>Gemini 1.5 Pro</b>")]:::agent
                Oracle[("<b>🧠 Oracle (Advisor)</b><br>役割: 設計・難問解決<br>Brain: <b>Gemini 1.5 Pro</b>")]:::agent
                Librarian[("<b>📚 Librarian (Researcher)</b><br>役割: ドキュメント調査<br>Brain: <b>Gemini 1.5 Flash</b>")]:::agent
                
                %% チーム内の連携
                Sisyphus -- "① 相談 (難易度高)" --> Oracle
                Sisyphus -- "② 調査依頼 (Background)" --> Librarian
                Oracle -.-> Sisyphus
                Librarian -.-> Sisyphus
            end
        end
    end

    subgraph Cloud [☁️ Google Cloud / LLM Provider]
        GeminiPro[gemini-1.5-pro]:::llm
        GeminiFlash[gemini-1.5-flash]:::llm
    end

    %% データの流れ
    User == "「この機能を実装して」" ==> Sisyphus
    Sisyphus -- "推論リクエスト" --> desc_oc
    Oracle -- "推論リクエスト" --> desc_oc
    Librarian -- "推論リクエスト" --> desc_oc

    desc_oc == "API Call" ==> GeminiPro
    desc_oc == "API Call" ==> GeminiFlash

    %% 凡例
    linkStyle default stroke-width:2px,fill:none,stroke:#333;
```