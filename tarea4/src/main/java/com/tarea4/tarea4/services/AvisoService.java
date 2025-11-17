package com.tarea4.tarea4.services;

import com.tarea4.tarea4.models.Aviso;
import com.tarea4.tarea4.models.Nota;
import com.tarea4.tarea4.models.AvisoRepository;
import com.tarea4.tarea4.models.NotaRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class AvisoService {
    private final AvisoRepository avisoRepository;
    private final NotaRepository notaRepository;

    public AvisoService(AvisoRepository avisoRepository, NotaRepository notaRepository) {
        this.avisoRepository = avisoRepository;
        this.notaRepository = notaRepository;
    }

    public List<Aviso> listarAvisos(){
        List<Aviso> avisos = avisoRepository.findAll();
        for(Aviso a : avisos) {
            List<Nota> notas = notaRepository.findByAviso(a);
            if(notas.isEmpty()) a.setPromedio(null);
            else a.setPromedio(notas.stream().mapToInt(Nota::getNota).average().orElse(0));
        }
        return avisos;
    }

    public void agregarNota(Integer idAviso, Integer notaValor){
        Aviso aviso = avisoRepository.findById(idAviso).orElseThrow();
        Nota nota = new Nota(aviso, notaValor);
        notaRepository.save(nota);

    }
    
}
