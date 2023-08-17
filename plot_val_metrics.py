import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_pickle("/home/flo/pacemaker/vsc_runs/distance_10_run/test_pred.pckl.gzip", compression="gzip") #TODO check this

lw=3
marker="^"
norm = "fro"
plt.scatter(df.index.values,df["forces"].apply(lambda x : np.linalg.norm(x, ord=norm)), label="true", s=lw, marker=marker,
            alpha=0.5, zorder=2)
plt.scatter(df.index.values, df["forces_pred"].apply(lambda x : np.linalg.norm(x, ord=norm)), label="pred", s=lw, marker=marker)


plt.legend()
plt.xlabel("structure index")
plt.ylabel("Force meV/A")
plt.title("True vs Predicted Values Norm: " + str(norm))
plt.show()

diff=df["forces"].abs()-df["forces_pred"].abs()
plt.scatter(df.index.values, diff.apply(lambda x : np.linalg.norm(x, ord=norm)), label="diff", s=lw, marker=marker)
plt.legend()
plt.xlabel("structure index")
plt.ylabel("diff Forces meV/A")
plt.title("diff True vs Predicted Values Norm: " + str(norm))
plt.show()

diff=df["forces"].abs()-df["forces_pred"].abs()
plt.scatter(df["forces"].apply(lambda x : np.linalg.norm(x, ord=norm)), diff.apply(lambda x : np.linalg.norm(x, ord=norm)), label="diff", s=lw, marker=marker)
plt.legend()
plt.xlabel("DFT Forces (|F| meV/A)")
plt.ylabel("diff Forces (|F| meV/A)")
plt.title("DFT vs Errors " + str(norm))
plt.show()


