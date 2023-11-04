using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FallenPlatform : MonoBehaviour
{
    public bool isReturnable = true;
    public Color activeColor;
    public float timeToFall = 1;
    public float timeToHide = 1;
    public float timeToReturn = 3;
    private Rigidbody2D rigidbody;
    private Color defaultColor;
    private Vector2 position;
    private Quaternion rotation;
    void Start()
    {
        activeColor.a = 1;
        defaultColor = GetComponent<SpriteRenderer>().color;
        if (GetComponent<Rigidbody2D>() == null)
        {
            rigidbody = gameObject.AddComponent<Rigidbody2D>();
            rigidbody.isKinematic = true;
        }

        rigidbody = gameObject.GetComponent<Rigidbody2D>();
        position = transform.position;
        rotation = transform.rotation;
    }
    void fall()
    {
        rigidbody.isKinematic = false;
        Invoke("inActive", timeToHide);
    }
    void inActive()
    {
        if (isReturnable)
        {
            gameObject.SetActive(false);
            Invoke("activate", timeToReturn);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    void activate()
    {
        gameObject.SetActive(true);
        GetComponent<Rigidbody2D>().isKinematic = true;
        transform.position = position;
        transform.rotation = rotation;
        GetComponent<SpriteRenderer>().color = defaultColor;
    }
    private void OnCollisionEnter2D(Collision2D collision)
    {
        if(collision.gameObject.tag=="Player")
        {
            GetComponent<SpriteRenderer>().color = activeColor;
            Invoke("fall", timeToFall);
        }
    }
}
