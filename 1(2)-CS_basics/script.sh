
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
#!/bin/bash
if ! command -v conda &> /dev/null; then
    echo "[INFO] Conda를 찾을 수 없습니다. Miniconda 설치를 진행합니다..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p "$HOME/miniconda"
    source "$HOME/miniconda/etc/profile.d/conda.sh"
    rm miniconda.sh
else
    # 이미 존재한다면 가상환경 활성화를 위해 프로파일 소싱
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
fi

# Conda 환셩 생성 및 활성화
## TODO
# 1. myenv라는 이름의 가상환경 생성 (파이썬 버전 3.10 지정)
if ! conda info --envs | grep -q "myenv"; then
    echo "[INFO] 'myenv' 가상환경을 생성합니다..."
    conda create -n myenv python=3.10 -y
fi
conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    prob_num=$(echo "$file" | cut -d'_' -f2 | cut -d'.' -f1)
    
    # 현재 위치가 submission/ 이므로 상위 디렉토리(../)의 input 및 output 참조
    input_file="../input/${prob_num}_input"
    output_file="../output/${prob_num}_output"
    
    if [ -f "$input_file" ]; then
        python "$file" < "$input_file" > "$output_file"
    else
        echo "[WARN] 입력 파일을 찾을 수 없습니다: $input_file"
    fi

done

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
mypy . > ../mypy_log.txt 2>&1
# conda.yml 파일 생성
## TODO
conda env export > ../conda.yml
# 가상환경 비활성화
## TODO
conda deactivate