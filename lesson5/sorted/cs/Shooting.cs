using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;

public class Shooting : MonoBehaviour{
     public  GameObject bullet ;
     public GameObject banger;
     public KeyCode ShootingKey; 
    public  int lifetime = 2 ;
    public float speed = 2 ;
    public  int currentBullets = 5 ;
    public  Text howManyBullets ;
    public  string tagOfAmmo =  "ammo" ;
    public int BulletsAmmo = 5 ;
    float move;

    void Start()
    {
        Vector3 theScale = bullet.transform.localScale;
        theScale.x = Mathf.Abs(theScale.x);
        bullet.transform.localScale = theScale;
        if (banger.transform.position.x - transform.position.x > 0)
            move = 1;
        else
            move = -1;
    }

    void Update()
    {
        if (banger.transform.position.x - transform.position.x > 0)
            move = 1;
        else
            move = -1;
        if (Input.GetKeyDown(ShootingKey) && currentBullets > 0)
        {
            GameObject ob = Instantiate(bullet, new Vector3(banger.transform.position.x, banger.transform.position.y,
                banger.transform.position.z), Quaternion.identity);
            Vector3 theScale = ob.transform.localScale;
            theScale.x *= move;
            ob.transform.localScale = theScale;
            Rigidbody2D rigidbody = ob.GetComponent<Rigidbody2D>();
            rigidbody.velocity = new Vector2(move * speed, 0);
            Destroy(ob, lifetime);
            currentBullets--;
        }

        howManyBullets.text = currentBullets.ToString();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if ( collision.gameObject.tag == tagOfAmmo)
        {
            currentBullets += BulletsAmmo;
            Destroy(collision.gameObject);







        }










    }














    }