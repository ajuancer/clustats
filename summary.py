import re
from matplotlib import pyplot as plt

data_path = "other.clustal_num"
f_seqs = []
seqs = []
t = None

class Sequence(object):
    def __init__(self, name, sequence, info, *args):
        self.sequence = sequence
        self.info = Sequence.convert(info, sequence)
        self.name = name
    def convert(original, length):
        return [1 if i == "*" else -1 for i in original[-len(length):]]

    def update_info(self):
        t = [i.start() for i in re.finditer('-', self.sequence)]
        [self.info.pop(a) for a in sorted(t, reverse=True)]
        self.sequence = self.sequence.replace("-", "")



with open(data_path, "r+") as f:
    f_seqs = f.readlines()[3:]  # skip header
f_seqs = [i for i in f_seqs if i != "\n"]
f_seqs = list(zip(*(iter(f_seqs),) * 3))

for i in f_seqs:
    match = False
    name, seq = re.split(r' +', i[0])
    seq = seq[:seq.find("\t")]
    for j, k in enumerate(seqs):
        if k.name == name:
            k.sequence += seq
            [k.info.append(s) for s in Sequence.convert(i[2], seq)]
            seqs[j] = k
            match = True
    if not match:
        seqs.append(Sequence(name, seq, i[2]))
    # seqs.append(Sequence(name, seq, i[2]))


    name, seq = re.split(r' +', i[1])
    seq = seq[:seq.find("\t")]
    # seqs.append(Sequence(name, seq, i[2]))
    for j, k in enumerate(seqs):
        if k.name == name:
            k.sequence += seq
            [k.info.append(s) for s in Sequence.convert(i[2], seq)]
            seqs[j] = k
            match = True
    if not match:
        seqs.append(Sequence(name, seq, i[2]))

seqs[0].update_info()
seqs[1].update_info()

# counter =0
# for i in seqs[0].info:
#     if i==1:
#         counter+=1

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Gene matching comparison')
ax1.set_title(seqs[0].name)
ax2.set_title(seqs[1].name)
width = .35

# get the -1 pos (no match)
for i, j in enumerate(seqs[0].info):
    if j == -1:
        ax1.axhline(y=i, color='r', linestyle='-')
    else:
        ax1.axhline(y=i, color='g', linestyle='-')

for i, j in enumerate(seqs[1].info):
    if j == -1:
        ax2.axhline(y=i, color='r', linestyle='-')
    else:
        ax2.axhline(y=i, color='g', linestyle='-')

# some styling
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.axes.get_xaxis().set_visible(False)
ax2.axes.get_xaxis().set_visible(False)
plt.show()
