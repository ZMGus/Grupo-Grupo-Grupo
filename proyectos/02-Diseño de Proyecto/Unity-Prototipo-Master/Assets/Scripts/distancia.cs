using UnityEngine;

public class distancia : MonoBehaviour
{
    public Transform jugador;
    public Transform objetivo;
    public float tiempo = 1.0f;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        tiempo -= Time.deltaTime;
        if (tiempo <= 0)
        {
            mensaje();
        }
        
    }
    public void mensaje()
    {   
        float distance = Vector3.Distance(jugador.position, objetivo.position);
        Debug.Log("Distance between objects: " + distance);
       //Debug.Log("El jugador ha llegado a la salida.");
    }
}
