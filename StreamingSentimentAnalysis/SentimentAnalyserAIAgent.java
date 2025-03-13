package com.striim.ai;

import com.webaction.anno.AdapterType;
import com.webaction.anno.PropertyTemplate;
import com.webaction.anno.PropertyTemplateProperty;
import com.webaction.runtime.BuiltInFunc;
import com.webaction.runtime.components.openprocessor.StriimOpenProcessor;
import com.webaction.runtime.containers.WAEvent;
import com.webaction.security.Password;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import dev.langchain4j.data.embedding.Embedding;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.output.Response;
import dev.langchain4j.model.openai.OpenAiLanguageModel;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import org.json.JSONObject;

@PropertyTemplate(name = "SentimentAnalyserAIAgent", type = AdapterType.process, properties = {
        @PropertyTemplateProperty(name = "apiKey", type = Password.class, required = true, defaultValue = ""),
        @PropertyTemplateProperty(name = "model", type = String.class, required = true, defaultValue = ""),
        @PropertyTemplateProperty(name = "TableAndColumns", type = String.class, required = true, defaultValue = "")
}, inputType = com.webaction.proc.events.WAEvent.class, outputType = com.webaction.proc.events.WAEvent.class)
public class SentimentAnalyserAIAgent extends StriimOpenProcessor {
    private static final long serialVersionUID = 1L;
    private static final Logger logger = LogManager.getLogger(SentimentAnalyserAIAgent.class);
    private Map<String, Object> properties;

    String tableName;
    public String[] columnNames;

    private OpenAiLanguageModel languageModel;
    @Override
    public void start() {
        properties = this.getProperties();
        if (properties.get("apiKey") == null) {
            throw new RuntimeException("apiKey not specified.");
        }
        if (properties.get("model") == null) {
            throw new RuntimeException("model not specified.");
        }
        if (properties.get("TableAndColumns") == null) {
            throw new RuntimeException("TableAndColumns not specified.");
        }

        String tableString = properties.get("TableAndColumns").toString().trim();
        setFetchColumns(tableString);

        // set up language model
        setupLanguageModel(((Password)properties.get("apiKey")).getPlain(), properties.get("model").toString());
    }

    @Override
    public Map getAggVec() {
        return properties;
    }

    @Override
    public void setAggVec(Map aggVec) {
        properties = aggVec;
    }

    private void setFetchColumns(String tableString) throws RuntimeException {
        try {
            tableName = tableString.substring(0, tableString.indexOf("("));
            String cols = tableString.substring(tableString.indexOf("(") + 1,
                    tableString.indexOf(")"));
            this.columnNames = cols.split(",");
        } catch (Exception e) {
            throw new RuntimeException("TableAndColumns not correctly specified");
        }
    }

    private void setupLanguageModel(String apiKey, String model) {
        try {
            languageModel = new OpenAiLanguageModel(null, apiKey, model, null, null, null, null, false, false);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void run() {
        Iterator<WAEvent> incomingEvents = getAdded().iterator();
        while (incomingEvents.hasNext()) {
            WAEvent thisEvent = incomingEvents.next();
            com.webaction.proc.events.WAEvent out = com.webaction.proc.events.WAEvent
                    .makeCopy((com.webaction.proc.events.WAEvent) thisEvent.data);
            try {
                if (!tableName.equalsIgnoreCase((String) out.metadata.get("TableName"))) {
                    continue;
                }
                String textInput = "";
                for (String fetchCol : columnNames) {
                    textInput += BuiltInFunc.GETDATA(out, fetchCol);
                }

                String prompt = String.format("You will be given a review for a store enclosed in triple backticks (```). " +
                        "Describe the sentiment of that review strictly as POSITIVE, NEUTRAL, or NEGATIVE. For example : * 'I love the staff': POSITIVE * 'This store is messy': NEGATIVE * 'Store was okay, nothing special.':NEUTRAL.```%s```",
                        textInput);
                // add the response to userdata
                String promptResponse = generatePromptResponse(prompt);
                out.putUserdata("reviewSentiment", promptResponse);
                send(out);
            } catch (Exception e) {
                logger.error("Error while generating the response ", e);
                send(out);
            }
        }
    }

    // Get prompt response
    private String generatePromptResponse(String input) throws IOException {
        //String prompt = String.format("You will be given a review for a product enclosed in triple backticks (```). Describe the sentiment of that review strictly as POSITIVE, NEUTRAL, or NEGATIVE. For example : * 'I love the product': POSITIVE * 'It is a scam': NEGATIVE * 'I tried the product':NEUTRAL.```%s```", input);
        String prompt = input;
        Response<String> response = languageModel.generate(prompt);
        System.out.println(input + " -------- " + response.content().trim());
        return response.content().trim();
    }
}
