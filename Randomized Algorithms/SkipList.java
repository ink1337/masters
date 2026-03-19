import java.util.Random;

/**
 * A Randomized Skip List implementation.
 * Provides O(log n) expected time for search and insertion.
 */
public class SkipList {
    // Maximum height allowed to prevent excessive memory usage
    private static final int MAX_LEVEL = 16;

    // Sentinel node (head) with no value, acting as the starting point for all levels
    private final Node head = new Node(-1, MAX_LEVEL);
    private final Random random = new Random();

    // Keeps track of the highest level currently containing nodes
    private int currentLevels = 0;

    /**
     * Determines the height of the new node tower using "Coin Flips".
     * Statistically, 50% of nodes reach level 1, 25% reach level 2, etc.
     */
    private int randomLevel() {
        int lvl = 0;
        // While "Heads" (true) and below limit, increase level
        while (random.nextBoolean() && lvl < MAX_LEVEL) {
            lvl++;
        }
        return lvl;
    }

    public void insert(int value) {
        // update[] stores the predecessors (nodes to the left) at each level
        Node[] update = new Node[MAX_LEVEL + 1];
        Node curr = head;

        // 1. Traverse from top to bottom to find the insertion position
        for (int i = currentLevels; i >= 0; i--) {
            // Move right as long as the next value is smaller than the target
            while (curr.next[i] != null && curr.next[i].value < value) {
                curr = curr.next[i];
            }
            // Capture the last node on this level before dropping down
            update[i] = curr;
        }

        // 2. Determine the height for the new node
        int lvl = randomLevel();

        // If the new node is taller than current list, update the 'update' array for higher levels
        if (lvl > currentLevels) {
            for (int i = currentLevels + 1; i <= lvl; i++) {
                update[i] = head;
            }
            currentLevels = lvl;
        }

        // 3. Create the new node and rewire the pointers
        Node newNode = new Node(value, lvl);
        for (int i = 0; i <= lvl; i++) {
            // Standard linked list insertion on level i:
            // New node points to the successor of the predecessor
            newNode.next[i] = update[i].next[i];
            // Predecessor now points to the new node
            update[i].next[i] = newNode;
        }
    }

    public boolean search(int target) {
        Node curr = head;
        // Traverse the levels from highest to lowest
        for (int i = currentLevels; i >= 0; i--) {
            // Skip over elements smaller than target
            while (curr.next[i] != null && curr.next[i].value < target) {
                curr = curr.next[i];
            }
        }

        // Final move: jump to the immediate next node on the base level (L0)
        curr = curr.next[0];

        // If the node exists and matches the target, we found it
        return curr != null && curr.value == target;
    }
}

/**
 * Node representing a "Tower" in the Skip List.
 */
class Node {
    int value;
    Node[] next; // Array of forward pointers for different levels

    public Node(int value, int level) {
        this.value = value;
        // next[0] is the base level, next[level] is the top of the tower
        this.next = new Node[level + 1];
    }
}