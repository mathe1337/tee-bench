import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def readable_names(x, str=None):
    modifier = "(" + str + ")" if str is not None else ""
    if "native" in x:
        return 'Plain CPU' + " " + modifier
    elif 'sgx' in x:
        return 'SGX Data in Enclave' + " " + modifier


def plot_mutex_timing():
    df_sgx = pd.read_csv("../data/wait_time_mutexsgx-output.csv")
    df_native = pd.read_csv("../data/wait_time_mutexnative-output.csv")
    df_sgx = pd.concat([df_sgx, pd.read_csv("../data/wait_time_mutexsgx-output-RSM.csv")])
    df_native = pd.concat([df_native, pd.read_csv("../data/wait_time_mutexnative-output-RSM.csv")])
    for algo in ['RHT', 'RHO', 'RSM']:
        df_sgx_temp = df_sgx[df_sgx['alg'] == algo]
        df_native_temp = df_native[df_native['alg'] == algo]
        df_temp = pd.concat([df_native_temp, df_sgx_temp], ignore_index=True)
        df_temp['mutexPercent'] = (df_temp['waitTimeMutex'] / df_temp['totalTime']) * 100
        df_temp['mode'] = df_temp['mode'].apply(lambda x: readable_names(x))

        g = sns.catplot(kind='box', data=df_temp, x="threads", y="mutexPercent", hue="mode", aspect=3,
                        palette=sns.color_palette(), legend_out=False)
        g.set(xlabel="Number of Threads", ylabel="Percentage of Runtime Spent on Mutex Acquisition")
        for ax in g.axes.ravel():
            for c in ax.containers:
                l = [f'{(v.get_height()):.2f}' for v in c]
                ax.bar_label(c, labels=l, label_type='center')
        plt.legend(title=None, loc=2)
        plt.tight_layout()
        plt.savefig('../img/time_spent_mutex' + algo + '.pdf')


def plot_spinlock_compare_mutex():
    df_spinlock_sgx = pd.read_csv("../data/wait_time_mutex_spinlocksgx-output.csv")
    df_mutex_sgx = pd.read_csv("../data/wait_time_mutexsgx-output.csv")
    df_spinlock_native = pd.read_csv("../data/wait_time_mutex_spinlocknative-output.csv")
    df_mutex_native = pd.read_csv("../data/wait_time_mutexnative-output.csv")
    for algo in ['RHT', 'RHO']:
        df_spinlock_sgx_temp = df_spinlock_sgx[df_spinlock_sgx['alg'] == algo].groupby(
            ['mode', 'alg', 'sizeR', 'sizeS', 'threads'], as_index=False).mean()
        df_mutex_sgx_temp = df_mutex_sgx[df_mutex_sgx['alg'] == algo].groupby(
            ['mode', 'alg', 'sizeR', 'sizeS', 'threads'], as_index=False).mean()
        df_spinlock_native_temp = df_spinlock_native[df_spinlock_native['alg'] == algo].groupby(
            ['mode', 'alg', 'sizeR', 'sizeS', 'threads'], as_index=False).mean()
        df_mutex_native_temp = df_mutex_native[df_mutex_native['alg'] == algo].groupby(
            ['mode', 'alg', 'sizeR', 'sizeS', 'threads'], as_index=False).mean()

        df_spinlock_sgx_temp['mode'] = 'Spinlock'
        df_mutex_sgx_temp['mode'] = 'Mutex'
        df_spinlock_sgx_temp['speedup'] = df_spinlock_native_temp['totalTime'] / df_spinlock_sgx_temp['totalTime']
        df_mutex_sgx_temp['speedup'] = df_mutex_native_temp['totalTime'] / df_mutex_sgx_temp['totalTime']
        df_temp = pd.concat([df_spinlock_sgx_temp, df_mutex_sgx_temp], ignore_index=True)
        g = sns.catplot(kind='bar', data=df_temp, x="threads", y="speedup", hue="mode", aspect=3,
                        edgecolor=".3", palette=sns.color_palette("pastel6"),
                        legend_out=False)
        g.set(xlabel="Number of Threads", ylabel="Throughput Compared to Native")
        for ax in g.axes.ravel():
            for c in ax.containers:
                l = [f'{(v.get_height()):.2f}' for v in c]
                ax.bar_label(c, labels=l, label_type='center')
        plt.legend(title=None, loc=2)
        plt.tight_layout()
        plt.savefig('../img/spinlock' + algo + '.pdf')


if False:
    def plot_spinlock_compare_sgx_native():
        df_spinlock_sgx = pd.read_csv("../data/wait_time_mutex_spinlocksgx-output.csv")
        df_spinlock_native = pd.read_csv("../data/wait_time_mutex_spinlocknative-output.csv")
        for algo in ['RHT', 'RHO']:
            df_spinlock_sgx_temp = df_spinlock_sgx[df_spinlock_sgx['alg'] == algo]
            df_spinlock_native_temp = df_spinlock_native[df_spinlock_native['alg'] == algo]
            df_spinlock_sgx_temp['mode'] = df_spinlock_sgx_temp['mode'].apply(lambda x: readable_names(x))
            df_spinlock_native_temp['mode'] = df_spinlock_native_temp['mode'].apply(lambda x: readable_names(x))
            df_spinlock_native_temp['slowdown'] = df_spinlock_native_temp['totalTime'] / df_spinlock_sgx_temp[
                'totalTime']
            g = sns.catplot(kind='bar', data=df_spinlock_native_temp, x="threads", y="mutexPercent", aspect=3,
                            edgecolor=".3",
                            palette=sns.color_palette(), legend_out=False, log=True)
            g.set(xlabel="Number of Threads", ylabel="% of Runtime Spent on Mutex Acquisition")
            for ax in g.axes.ravel():
                for c in ax.containers:
                    l = [f'{(v.get_height()):.2f}' for v in c]
                    ax.bar_label(c, labels=l, label_type='center')
            # plt.savefig('time_spend_on_mutex')
            plt.legend(title=None, loc=2)
            plt.tight_layout()
            plt.show()

if __name__ == '__main__':
    #plot_mutex_timing()
    plot_spinlock_compare_mutex()
