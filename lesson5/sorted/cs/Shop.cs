using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class Shop : MonoBehaviour
{
    public Text textOb;
    public string sellerText;
    public GameObject itemPrefab;
    public KeyCode keyToBuy;
    public int cost = 1;
    public GameObject genPlace;
    bool inside = false;
    private void Update()
    {
        if (Input.GetKeyDown(keyToBuy) && inside)
        {
            if (MoneyCollector.money > cost)
            {
                Vector3 v = new Vector3(Random.Range(-0.2f, 0.2f), Random.Range(-0.1f, 0.1f),0);
                Instantiate(itemPrefab, genPlace.transform.position+v,Quaternion.identity);
                MoneyCollector.money -= cost;
            }
            else
                textOb.text = "МАЛО ДЕНЕГ!!!";
        }
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "Player")
        {
            textOb.text += sellerText;
            inside = true;
        }
    }
    private void OnTriggerExit2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "Player")
        {
            textOb.text = "";
            inside = false;
        }
    }
}

