import os
import glob
import filecmp
import difflib

# ====================[ 경로 설정 ]====================
DIR1 = r"C:\PL\tree-sitter-smallbasic\SB_Data_TS1"
DIR2 = r"C:\PL\tree-sitter-smallbasic\SB_Data_TS2"
DIFF_LOG_FILE = "diff_report.txt"  # 상세 차이점을 기록할 파일
# =========================================================

def main():
    if not os.path.exists(DIR1):
        print(f"[Error] Directory not found: {DIR1}")
        return
    if not os.path.exists(DIR2):
        print(f"[Error] Directory not found: {DIR2}")
        return

    # DIR1에 있는 모든 .data 파일 목록 가져오기
    files1 = {os.path.basename(f) for f in glob.glob(os.path.join(DIR1, "*.data"))}
    files2 = {os.path.basename(f) for f in glob.glob(os.path.join(DIR2, "*.data"))}

    all_files = sorted(files1.union(files2))
    
    identical_count = 0
    different_count = 0
    missing_count = 0

    print(f"[*] Starting comparison between TS1 and TS2 folders...")
    print(f"[*] Total unique files found: {len(all_files)}\n")

    with open(DIFF_LOG_FILE, "w", encoding="utf-8") as log:
        log.write("=== Diff Report ===\n")
        log.write(f"DIR1 ( - ): {DIR1}\n")
        log.write(f"DIR2 ( + ): {DIR2}\n\n")

        for filename in all_files:
            file1_path = os.path.join(DIR1, filename)
            file2_path = os.path.join(DIR2, filename)

            # 1. 파일 누락 체크
            if filename not in files1:
                print(f"[?] {filename}: Only exists in TS2")
                log.write(f"\n[Missing] {filename} is missing in TS1.\n")
                missing_count += 1
                continue
            if filename not in files2:
                print(f"[?] {filename}: Only exists in TS1")
                log.write(f"\n[Missing] {filename} is missing in TS2.\n")
                missing_count += 1
                continue

            # 2. 파일 내용 비교 (단순 일치 여부 빠른 확인)
            if filecmp.cmp(file1_path, file2_path, shallow=False):
                print(f"[OK] {filename}: Identical")
                identical_count += 1
            else:
                # 3. 내용이 다를 경우 상세 비교 (Diff 생성)
                print(f"[Diff] {filename}: Different! (Check {DIFF_LOG_FILE})")
                different_count += 1
                
                with open(file1_path, 'r', encoding='utf-8') as f1, \
                     open(file2_path, 'r', encoding='utf-8') as f2:
                    lines1 = f1.readlines()
                    lines2 = f2.readlines()

                # Unified Diff 형식으로 차이점 계산
                diff = difflib.unified_diff(
                    lines1, lines2, 
                    fromfile=f"TS1/{filename}", 
                    tofile=f"TS2/{filename}", 
                    lineterm=''
                )

                log.write(f"\n========================================\n")
                log.write(f"[*] Differences in {filename}:\n")
                log.write(f"========================================\n")
                for line in diff:
                    log.write(line + "\n")

    # 최종 요약 출력
    print("\n==============================")
    print("      Comparison Summary      ")
    print("==============================")
    print(f" - Identical files : {identical_count}")
    print(f" - Different files : {different_count}")
    print(f" - Missing files   : {missing_count}")
    print(f" - Total files     : {len(all_files)}")
    print("==============================")
    
    if different_count > 0:
        print(f"\n[*] Detailed differences have been saved to '{DIFF_LOG_FILE}'.")

if __name__ == "__main__":
    main()