using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MoneyCollector : MonoBehaviour
{
    public static int money = 0;
    public string tagOfMoney;
    public int moneyValue = 5;
    public Text textOb;

    private void Update()
    {
        textOb.text = money.ToString();
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == tagOfMoney)
        {
            Destroy(collision.gameObject);
            money += moneyValue;
        }
    }
}


