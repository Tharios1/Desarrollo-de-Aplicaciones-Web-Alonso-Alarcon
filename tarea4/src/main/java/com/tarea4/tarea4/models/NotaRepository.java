package com.tarea4.tarea4.models;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface NotaRepository extends JpaRepository<Nota, Integer> {
    List<Nota> findByAviso(Aviso aviso);
    
}
