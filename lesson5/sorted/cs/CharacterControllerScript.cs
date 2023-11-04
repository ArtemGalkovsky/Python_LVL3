using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class CharacterControllerScript : MonoBehaviour
{
    Rigidbody2D rigidBody;
    public float moveSpeed = 10f;
    public float jumpForce = 500f;
    public bool doubleJump;
    bool isFacingRight = true;
    Animator anim;
    bool isGrounded = false;
    public Transform groundCheck;
    float groundRadius = 0.2f;
    int jumps;

    public LayerMask whatIsGround;
    private bool onLadder = false;
    public LayerMask whatIsLadder;
    void OnTriggerStay(Collider2D collision)
    {
        if ((1 << collision.gameObject.layer) == whatIsLadder)
        {
            onLadder = false;
            rigidBody.velocity = new  Vector2(rigidBody.velocity.x,rigidBody.velocity.y/5);
            anim.Play("Ladder");
            rigidBody.gravityScale = 1;
        }
    }

    void Ladder()
    {
        float vMove = Input.GetAxis("Vertical");
        float move = Input.GetAxis("Horizontal");
        if (move == 0 && vMove == 0)
            anim.speed = 0;
        else
            anim.speed = 1;
        rigidBody.velocity = new Vector2(rigidBody.velocity.x, vMove * moveSpeed);
    }
    void Start()
    {
        anim = GetComponent<Animator>();
        rigidBody = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Run();
        anim.SetBool("Ladder",onLadder);
        if (onLadder)
            Ladder();
        isGrounded = Physics2D.OverlapCircle(groundCheck.position, groundRadius, whatIsGround);
        anim.SetBool("Ground", isGrounded);
        anim.SetFloat("vSpeed", rigidBody.velocity.y);
        if (!isGrounded)
            return;
        else
            jumps = 0;
    }



    public void Run()
    {




        float move = Input.GetAxis("Horizontal");
        anim.SetFloat("Speed", Mathf.Abs(move));


        rigidBody.velocity = new Vector2(move * moveSpeed, rigidBody.velocity.y);
        if (move > 0 && !isFacingRight)
            Flip();
        else if (move < 0 && isFacingRight)
            Flip();
    }

    void Flip()
    {

        isFacingRight = !isFacingRight;

        Vector3 theScale = transform.localScale;

        theScale.x *= -1;

        transform.localScale = theScale;
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space)&&isGrounded)
    
            rigidBody.AddForce(new Vector2(0, jumpForce));
        
        else if (Input.GetKeyDown(KeyCode.Space)&&doubleJump&&jumps==0)
        	
            rigidBody.AddForce(new Vector2(0, jumpForce));
	    jumps=1;
        
    }
}