package com.tarea4.tarea4.models;
import jakarta.persistence.*;
@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String nombre;

    public String getNombre() { return nombre;}
    
}
