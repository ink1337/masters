import textwrap

import matplotlib.pyplot as plt

hypotheses = {
    "even": {"values": [i for i in range(2, 101, 2)], "prior_probability": 0.2},
    "odd": {"values": [i for i in range(1, 101, 2)], "prior_probability": 0.2},
    "multiples of 4": {"values": [i for i in range(4, 101, 4)], "prior_probability": 0.15},
    "multiples of 8": {"values": [i for i in range(8, 101, 8)], "prior_probability": 0.1},
    "multiples of 16": {"values": [i for i in range(16, 101, 16)], "prior_probability": 0.1},
    "powers of two": {"values": [2, 4, 8, 16, 32, 64], "prior_probability": 0.1},
    "powers of 2 except for 32": {"values": [2, 4, 8, 16, 64], "prior_probability": 0.1},
    "powers of 2 except for 32 and 64": {"values": [2, 4, 8, 16], "prior_probability": 0.05},
}


def prior(name_of_hypothesis: str) -> float:
    if name_of_hypothesis not in hypotheses:
        raise ValueError(f"Hypothesis {name_of_hypothesis} not found.")

    return hypotheses[name_of_hypothesis]["prior_probability"]


def calculate_likelihood(name_of_hypothesis: str, data_points: list[int]) -> float:
    if name_of_hypothesis not in hypotheses:
        raise ValueError(f"Hypothesis {name_of_hypothesis} not found.")
    hyp_values = hypotheses[name_of_hypothesis]["values"]
    for d in data_points:
        if d not in hyp_values:
            return 0.0
    size_h = len(hyp_values)
    return 1 / size_h ** len(data_points)
    # todo implement


def calculate_posterior(data_points: list[int]) -> dict[str, float]:
    unnormalized_values = {}
    sum = 0
    for h_name in hypotheses:
        prob = calculate_likelihood(h_name, data_points) * prior(h_name);
        unnormalized_values[h_name] = prob
        sum += prob
    if sum == 0:
        return {h_name: 0.0 for h_name in hypotheses}
    return {h_name: v / sum for h_name, v in unnormalized_values.items()}


def calculate_posterior_predictive(posterior_: dict[str, float]) -> dict[int, float]:
    predictive = {i: 0 for i in range(1, 101)}
    for h_name, posterior_prop in posterior_.items():
        if posterior_prop > 0:
            h_values = hypotheses[h_name]["values"]
            prop_next = 1/len(h_values)
            for val in h_values:
                predictive[val] += prop_next * posterior_prop
    return predictive


### == Do not change anything below this line (with the exception of `all_data`) ==


def sanity_check() -> None:
    sum_of_prior_probabilities = sum(
        properties["prior_probability"] for properties in hypotheses.values()
    )
    if sum_of_prior_probabilities != 1.0:
        raise ValueError("Prior probabilities are not normalized.")


def create_posterior_figure():
    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 6),
        gridspec_kw={"width_ratios": [1, 1.2]},
    )
    return fig, ax1, ax2


def plot_posterior(
        hypothesis_and_probabilities: dict[str, float],
        observed_data: list[int],
        ax,
        max_label_width: int = 40,
):
    labels = list(hypothesis_and_probabilities.keys())
    values = list(hypothesis_and_probabilities.values())

    wrapped_labels = [
        "\n".join(textwrap.wrap(label, max_label_width)) for label in labels
    ]

    bars = ax.barh(range(len(values)), values)

    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(wrapped_labels)
    ax.invert_yaxis()

    ax.set_xlabel("Posterior probability")
    ax.set_title(f"Posterior\nObserved data: {observed_data}")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{value * 100:.1f}%",
            va="center",
            ha="left",
            fontsize=9,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.5)


def plot_posterior_predictive(
        posterior_predictive_dist: dict[int, float],
        ax,
):
    xs = list(posterior_predictive_dist.keys())
    ps = list(posterior_predictive_dist.values())

    ax.bar(xs, ps)

    ax.set_xlabel("Number")
    ax.set_ylabel("Probability")
    ax.set_title("Posterior predictive")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.5)


if __name__ == "__main__":
    # feel free to modify `all_data` and provide different numbers to see how that changes
    # the posterior and the posterior predictive
    # all_data = [16, 8, 40, 50]
    all_data = [16, 8, 2, 64, 32]
    sanity_check()

    observed_data = []
    for new_datapoint in all_data:
        observed_data.append(new_datapoint)

        posterior = calculate_posterior(observed_data)
        posterior_predictive = calculate_posterior_predictive(posterior)

        fig, ax1, ax2 = create_posterior_figure()
        plot_posterior(posterior, observed_data, ax=ax1)
        if posterior_predictive is not None:
            plot_posterior_predictive(posterior_predictive, ax=ax2)

        plt.tight_layout()
        plt.show()
