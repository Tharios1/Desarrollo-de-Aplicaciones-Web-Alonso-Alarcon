package com.tarea4.tarea4.controllers;

import com.tarea4.tarea4.services.AvisoService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;

@Controller
public class AvisoController {

    private final AvisoService service;

    public AvisoController(AvisoService service){
        this.service = service;
    }

    @GetMapping("/")
    public String index(Model model){
        model.addAttribute("avisos", service.listarAvisos());
        return "index";
    }

    @PostMapping("/nota")
    @ResponseBody
    public String agregarNota(@RequestParam Integer id, @RequestParam Integer nota){
        service.agregarNota(id, nota);
        return "OK";
    }
}





