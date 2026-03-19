import numpy as np
import matplotlib.pyplot as plt


def exp_cdf(x, l):
    """
    Value of the exponential cumulative distribution function for the provided values of x and lambda.
    """
    return 1 - np.exp(-l * x)


def exp_quantile(p, l):
    """
    Value of the exponential quantile function for the provided values of x and lambda.
    """
    return -np.log(1 - p) / l


def inverse_cdf_sampling(n, l, rng=None):
    """
    Implements the inverse CDF sampling by drawing n uniform numbers and then applying the inverse CDF.
    """
    if rng is None:
        rng = np.random.default_rng()

    u = rng.uniform(0, 1, n)
    x = exp_quantile(u, l)
    return x, u


def plot_inverse_cdf(n, l):
    # Pobieramy próbki (x) oraz wartości u, z których powstały
    x, u = inverse_cdf_sampling(n, l)

    # Przygotowujemy dane do wykresu teoretycznej krzywej CDF
    x_theory = np.linspace(0, max(x), 1000)
    y = exp_cdf(x_theory, l)

    plt.figure(figsize=(10, 6))

    # Rysujemy ciągłą linię dystrybuanty
    plt.plot(x_theory, y, "r-", label="True CDF (Teoretyczna)", zorder=1)

    # Rysujemy punkty (x, u) - zobaczysz, że idealnie układają się na linii!
    plt.scatter(x, u, s=12, alpha=0.5, label="Inverse CDF samples (Próbki)", zorder=2)

    plt.title(f"Sampling przez odwrotną dystrybuantę (lambda={l}, n={n})")
    plt.xlabel("Wartość wygenerowana (x)")
    plt.ylabel("Wylosowane prawdopodobieństwo (u)")
    plt.legend()
    plt.grid(True, alpha=0.3)


if __name__ == "__main__":
    plot_inverse_cdf(n=100, l=1.)
    plt.show()
