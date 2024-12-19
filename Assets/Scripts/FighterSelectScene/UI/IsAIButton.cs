﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class IsAIButton : MonoBehaviour
{
    public bool isAI;
    public Button button;

    Text buttonText;

    private void Awake()
    {
        button = GetComponent<Button>();
        buttonText = button.GetComponentInChildren<Text>();
    }
    private void Start()
    {
        isAI = true;
        buttonText.text = "Is AI";
        button.onClick.AddListener(ChangeIsAI);
    }
    void ChangeIsAI()
    {
        isAI = !isAI;
        if(isAI)
        {
            buttonText.text = "Is AI";
        }
        else
        {
            buttonText.text = "Is Player";
        }
    }
}