using UnityEngine;

public class checkTriggers : MonoBehaviour
{
    public string ID = "Don Juan";
    private CharacterController controller;
    private Rigidbody2D rb;
    public float speed = 5f;
    private Vector2 movementDirection;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        controller = GetComponent<CharacterController>();
        rb = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        float x = Input.GetAxis("Horizontal");
        float y = Input.GetAxis("Vertical");
        movementDirection = new Vector2(x, y).normalized;
    }

    void FixedUpdate()
    {
        rb.linearVelocity = movementDirection * speed;
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("salida"))
        {
            Debug.Log("El jugador " + ID + " ha llegado a la salida.");
            //--------------------------Broker aca-------------------------
        }
    }
}
