"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { toast } from "sonner";

interface BadgeData {
  name: string;
  markdown: string;
  markdown_code: string;
}

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [generatedBadges, setGeneratedBadges] = useState<BadgeData[]>([]);
  const [invalidSlugs, setInvalidSlugs] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const generateBadges = async () => {
    const slugs = inputText.split(",").map((slug) => slug.trim());

    if (!slugs.length || (slugs.length === 1 && !slugs[0])) {
      toast.error("Please enter comma-separated simple-icons slugs.");
      return;
    }

    setIsLoading(true);
    setGeneratedBadges([]);
    setInvalidSlugs([]);

    try {
      const response = await fetch(
        "http://localhost:5000/generate_badges", // Use the correct API endpoint
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ slugs }), // Send the array of slugs
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData?.error ||
            `Failed to generate badges (HTTP ${response.status})`
        );
      }

      const data = await response.json();
      setGeneratedBadges(data.badges);
      setInvalidSlugs(data.invalid_slugs);

      toast.success("Badges generated successfully!");
    } catch (error: unknown) {
      console.error("Error generating badges:", error);
      if (error instanceof Error) {
        toast.error(
          error.message || "Failed to generate badges. Please try again."
        );
      } else {
        toast.error("An unknown error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">
              Markdown Badge Generator
            </CardTitle>
            <CardDescription className="text-center">
              Enter comma-separated simple-icons slugs to generate badges.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="input-text" className="text-sm font-medium">
                  Simple-Icons Slugs
                </label>
                <Input
                  id="input-text"
                  placeholder="e.g., react, nextdotjs, github"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && generateBadges()}
                />
              </div>

              <Button
                onClick={generateBadges}
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? "Generating..." : "Generate Badges"}
              </Button>

              {generatedBadges.length > 0 && (
                <div className="mt-6 space-y-2">
                  <h3 className="text-sm font-medium">Generated Badges:</h3>
                  <ul className="space-y-2">
                    {generatedBadges.map((badge) => (
                      <li key={badge.name} className="break-words">
                        <code>{badge.markdown}</code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {invalidSlugs.length > 0 && (
                <div className="mt-4 space-y-2">
                  <h3 className="text-sm font-medium text-red-500">
                    Invalid Slugs:
                  </h3>
                  <ul className="list-disc pl-5">
                    {invalidSlugs.map((slug) => (
                      <li key={slug} className="text-red-500 break-words">
                        {slug}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
