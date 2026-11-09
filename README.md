# PushSwap

## English

A C program that prints instructions for sorting integers in ascending order. It uses two stacks and a restricted set of swaps, moves, and rotations. A stack is a container whose topmost value is taken out first.

All values start in stack A; stack B is empty. The program prints one instruction per line to sort A. The goal is to use few instructions.

### Build and run

Requires a C compiler and Make.

```sh
make
./push_swap 2 1 3
```

This prints `sa`: swap the first two values in A. Applying it gives `1 2 3`.

Duplicates, non-integers, and values outside the `int` range produce `Error` on standard error. No instructions are printed for empty or already sorted input.

### Options

| Flag | Behavior |
| --- | --- |
| `--adaptive` | Choose a strategy from input size and disorder; the default |
| `--simple` | Move the smallest values in order, similar to selection sort |
| `--medium` | Move ranked values in chunks |
| `--complex` | Sort ranked values by bits using radix sort |
| `--bench` | Print disorder, strategy, and operation counts to standard error |

Inputs of five or fewer values use dedicated small-input routines regardless of the selected strategy.

```sh
./push_swap --bench --medium 8 4 7 3 6 2 5 1
```

### Check the instructions

The `checker` program accepts the same integers and the generated instructions. It prints `OK` if they sort the input, or `KO` otherwise.

```sh
make bonus
./push_swap 4 67 3 87 23 | ./checker 4 67 3 87 23
```

### Implementation

- Replaces input values with their ascending ranks so negative and large integers use the same sorting routines.
- Automatic selection switches between Simple, Chunk, and Radix strategies using size and disorder thresholds.

### Tests

```sh
make test
```

An independent stack interpreter checks all four strategies, empty input, duplicates, integer limits, invalid values, and the checker.

## 日本語

与えられた整数を小さい順に並べるための操作手順を出力するCプログラムです。2つのスタックを使い、交換・移動・回転という決められた操作だけで整列します。スタックは、上に積んだ値から取り出す入れ物です。

最初は全ての値がスタックAにあり、Bは空です。Aを昇順にする命令を1行ずつ出力します。少ない命令で整列することが課題の中心です。

### ビルドと実行

Cコンパイラ・Make が必要です。

```sh
make
./push_swap 2 1 3
```

この例では `sa` と1行表示します。これは「Aの先頭2個を交換する」という命令で、適用すると `1 2 3` になります。

重複・整数以外の値・`int` の範囲外の値は、標準エラー出力に `Error` を表示します。引数がない場合や整列済みの場合は、命令を出力しません。

### オプション

| フラグ | 動作 |
| --- | --- |
| `--adaptive` | 要素数と乱雑度から戦略を選ぶ（デフォルト） |
| `--simple` | 最小要素を順に移す選択ソート系の戦略 |
| `--medium` | 値の順位を範囲ごとに分けて移すチャンクソート |
| `--complex` | 値の順位をビットごとに処理する基数ソート |
| `--bench` | 乱雑度・戦略・操作数を標準エラー出力に表示 |

要素数が5以下の場合は、戦略の指定にかかわらず専用の小規模ソートを使います。

```sh
./push_swap --bench --medium 8 4 7 3 6 2 5 1
```

### 検証

命令の検証用プログラム `checker` に、同じ整数列と生成した命令を渡すと、整列できた場合は `OK`、できなかった場合は `KO` を表示します。

```sh
make bonus
./push_swap 4 67 3 87 23 | ./checker 4 67 3 87 23
```

### 実装メモ

- 入力値を昇順の順位に変換し、負の数や大きな整数も同じソート処理で扱います。
- 自動選択では要素数と乱雑度のしきい値を使い、Simple・Chunk・Radix を切り替えます。
### テスト

```sh
make test
```

4戦略の整列結果を独立したスタック処理で検証し、空入力・重複・整数境界値・不正な値・checkerを確認します。
