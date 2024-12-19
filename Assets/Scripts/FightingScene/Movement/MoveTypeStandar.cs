using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveTypeStandar : MonoBehaviour, IMove
{
    public InputInfo inputInfo;

    Rigidbody2D rb;
    FighterController fighterController;
    Rotator rotator;

    void Awake()
    {
        fighterController = GetComponent<FighterController>();
        rb = GetComponent<Rigidbody2D>();
    }

    void Start()
    {
        rotator = new Rotator(transform, GetComponent<FighterController>().side);
    }
    public void MoveInXAxis(float speed)
    {
        if (!MoveRequested()) return;
        rb.linearVelocity = new Vector2(GetXAxis() * speed * Time.deltaTime, rb.linearVelocity.y);
    }
    public bool MoveRequested()
    {
        return inputInfo.InputPulsed();
    }
    public float GetXAxis()
    {
        float xAxis = 0;

        switch (rotator.currentSideFacing)
        {
            case FighterSide.right:
                if (inputInfo.MoveToLeftRequested())
                {
                    rotator.currentSideFacing = FighterSide.left;
                    xAxis = -2;
                }
                else xAxis = 2;
                break;
            case FighterSide.left:
                if (inputInfo.MoveToRightRequested())
                {
                    rotator.currentSideFacing = FighterSide.right;
                    xAxis = 2;
                }
                else xAxis = -2;
                break;
        }

        return xAxis;
    }

    public void Jump(float jumpForce)
    {
        rb.AddForce(new Vector2(0, jumpForce));
    }

    public bool JumpRequested()
    {
        return Input.GetKeyDown(fighterController.info.jumpKey);
    }

    public bool BlockRequested()
    {
        return Input.GetKeyDown(fighterController.info.blockKey);
    }
}
