import numpy as np
import matplotlib.pyplot as plt

class Sequence:
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence.upper()   # vždy uložíme velkými písmeny

    def length(self):
        return len(self.sequence)

    def __str__(self):
        return f"[{self.name}] délka={self.length()} nt, začátek: {self.sequence[:8]}..."


seq = Sequence("testovací", "acgtagctagc")
print(seq)            # [testovací] délka=11 nt, začátek: ACGTAGCT...
print(seq.length())   # 11
print(seq.sequence)   # ACGTAGCTAGC – automaticky převedeno na velká písmena


class DNASequence(Sequence):
    def gc_content(self):
        gc = self.sequence.count("G") + self.sequence.count("C")
        return gc / len(self.sequence)

    def base_counts(self):
        a=self.sequence.count("A")
        t=self.sequence.count("T")
        g=self.sequence.count("G")
        c=self.sequence.count("C")
        final_dict = {"A":a, "T":t, "G":g, "C":c}
        return final_dict

    def plot_composition(self):
        counts = self.base_counts()
        bases = ["A", "C", "G", "T"]
        values = [counts[b] for b in bases]
        colors = ["tab:green", "tab:blue", "tab:orange", "tab:red"]

        plt.figure(figsize=(5, 3))
        plt.bar(bases, values, color=colors, edgecolor="black")
        plt.title(f"Složení bází: {self.name}")
        plt.ylabel("Počet")
        plt.tight_layout()
        plt.show()

    def is_valid(self):
        return set(self.sequence) <= {"A", "C", "G", "T"}

    def to_rna(self):
        return RNASequence(self.name, self.sequence.replace("T", "U"))

class RNASequence(Sequence):
    def is_valid(self):
        return set(self.sequence) <= {"A", "C", "G", "U"}

    def codons(self):
        return [self.sequence[i:i+3] for i in range(0, len(self.sequence) - 2, 3)]

    def find_start_codon(self):
        letters = self.sequence
        return letters.find("AUG")


dna = DNASequence("mini", "ACCGGGTT")
print(dna.base_counts())  # {"A": 1, "C": 2, "G": 3, "T": 2}
dnaH = DNASequence("maxi", "ACCGGGTTACGGTTCCAAGGTTCCA")
dna.plot_composition()
dnaH.plot_composition()

dna1 = DNASequence("platná",   "ACGCTAGCTAGC")
dna2 = DNASequence("neplatná", "ACGCNTAGCTAGC")   # N = neznámá báze

print(dna1.is_valid())   # True
print(dna2.is_valid())   # False

print(RNASequence("správná",   "ACGUACGU").is_valid())  # True
print(RNASequence("s thyminem","ACGTACGU").is_valid())  # False — T v RNA být nemá

rna = RNASequence("mini", "AUGGCUUAA")
print(rna.codons())   # ["AUG", "GCU", "UAA"]
rna2 = RNASequence("zbytek", "AUGGCUUA")
print(rna2.codons())  # ["AUG", "GCU"]   — poslední dvě písmena netvoří celý kodon

find_rna = RNASequence("gen", "CCAUGGCUUAA")
print(find_rna.find_start_codon())   # 2   — AUG začíná na indexu 2
