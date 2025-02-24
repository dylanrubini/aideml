#!/bin/bash

micromamba deactivate
micromamba activate aide_agent

allowed_models=("gpt-4o-mini" "qwen2.5")
model="$@"

echo "Model requested = ${model}"

found=0
for item in "${allowed_models[@]}"; do
    if [[ "$model" == "$item" ]]; then
        found=1
        break
    fi
done

found=0

for item in "${allowed_models[@]}"; do

    if [[ "$model" == "$item" ]]; then
        found=1
        break
    fi
done

if [[ $found -eq 1 ]]; then
    echo "✅ Model '$model' is allowed."
else
    echo "🚨 Model '$model' is NOT allowed."
    return 1
fi


if [[ "$model" == "qwen2.5" ]]; then 
	if command -v ollama &> /dev/null; then
	    echo "✅ Ollama is available."
	else
	    echo "🚨 Ollama is NOT installed or not in PATH."
	    return 1
	fi

	# Check if Ollama service is running on port 11434
	if curl -s http://localhost:11434/v1/models &> /dev/null; then
	    echo "✅ Ollama is already running."
	else
	    echo "⚠️ Ollama is NOT running. Starting it now..."
	    ollama serve &  # Start Ollama in the background
	    sleep 3  # Wait a few seconds for it to start
	    echo "✅ Ollama started successfully!"
	fi

	export OPENAI_BASE_URL="http://localhost:11434/v1"
	export OPENAI_API_KEY="qwen2.5"

	echo "-----------------------------------------------------------"
	echo "Local host is = ${OPENAI_API_KEY}"
	echo "-----------------------------------------------------------"

else 

	unset OPENAI_BASE_URL
	export OPENAI_API_KEY=$(awk -F '=' '/^OPENAI_API_KEY/ {print $2}' .env)

	echo "-----------------------------------------------------------"
	echo "The OpenAI Key for the API is = ${OPENAI_API_KEY}"
	echo "-----------------------------------------------------------"

fi

# Detect OS type
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/model: .*/model: $model/" ./utils/config.yaml  # macOS
else
    sed -i "s/model: .*/model: $model/" ./utils/config.yaml  # Linux
fi

python trial_run.py
# python trial_run.py --log-level DEBUG
