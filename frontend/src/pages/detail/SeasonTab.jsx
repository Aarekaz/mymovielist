import * as React from "react";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { Button } from "@mui/material";

export default function SeasonTab({ seasons, id }) {
  const [value, setValue] = React.useState("1");

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: "100%", typography: "body1" }}>
      <TabContext value={value}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <TabList
            onChange={handleChange}
            style={{ background: "white" }}
            aria-label="lab API tabs example"
          >
            {seasons?.map((item, index) => (
              <Tab label={item.name} value={index + 1} />
            ))}
          </TabList>
        </Box>
        {seasons?.map((item, index) => (
          <TabPanel value={index + 1}>
            {new Array(item.episode_count).fill("").map((item, idx) => (
              <Button
                style={{
                  margin: "2px",
                  backgroundColor: "#cc0000",
                  textTransform: "none",
                }}
                variant="contained"
                onClick={() => {
                  window.open(
                    "https://www.2embed.ru/embed/tmdb/tv?id=" +
                      id +
                      `&s=${index + 1}&e=${idx + 1}`
                  );
                }}
              >
                Episode {idx + 1}
              </Button>
            ))}
          </TabPanel>
        ))}
      </TabContext>
    </Box>
  );
}
